#!/usr/bin/env python3
"""
SMS Alert Sender Script
=======================
A production-practical, secure, and robust script to send SMS alerts to 
multiple recipients with support for rate-limiting, concurrency, retries, 
and input normalization.

Setup & Usage:
--------------
1. Create a virtual environment & install dependencies:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt

2. Configure secrets:
   cp .env.example .env
   # Edit .env with your actual Twilio credentials

3. Run the script:
   python sms_sender.py --sender +1234567890 --recipients-file recipients.txt --message "Alert from {sender} at {time}" --dry-run
"""

import os
import sys
import re
import time
import argparse
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

# Load environment variables safely
from dotenv import load_dotenv
load_dotenv()

# --- Logging Setup ---
logger = logging.getLogger("SmsSender")
logger.setLevel(logging.INFO)

# Console Handler
c_handler = logging.StreamHandler(sys.stdout)
c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

# Rotating File Handler (Max 5MB, keeping 3 backups)
f_handler = RotatingFileHandler("sms_sender.log", maxBytes=5*1024*1024, backupCount=3)
f_format = logging.Formatter('%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


# --- Provider Abstraction Layer ---
class SmsProvider(ABC):
    @abstractmethod
    def send_sms(self, to_number: str, from_number: str, body: str) -> bool:
        """Sends an SMS. Should throw an exception or return False on failure."""
        pass


class TwilioProvider(SmsProvider):
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN in environment.")
        
        # Deferred import to prevent crash if library isn't present during dry-runs
        from twilio.rest import Client
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, to_number: str, from_number: str, body: str) -> bool:
        try:
            message = self.client.messages.create(
                body=body,
                from_=from_number,
                to=to_number
            )
            logger.debug(f"Twilio message queued successfully. SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Twilio API Error sending to {to_number}: {str(e)}")
            raise e


class DryRunProvider(SmsProvider):
    def send_sms(self, to_number: str, from_number: str, body: str) -> bool:
        logger.info(f"[DRY-RUN] Sending SMS From: {from_number} | To: {to_number} | Body: {body}")
        time.sleep(0.05)  # Simulate a tiny network latency
        return True


# --- Rate Limiter Module ---
class ThreadSafeRateLimiter:
    """Coordinates message intervals across multiple threads safely."""
    def __init__(self, rate_per_sec: float):
        self.rate = rate_per_sec
        self.lock = threading.Lock()
        self.last_send_time = 0.0

    def wait_if_needed(self):
        if self.rate <= 0:
            return
        delay = 1.0 / self.rate
        with self.lock:
            now = time.time()
            elapsed = now - self.last_send_time
            if elapsed < delay:
                sleep_time = delay - elapsed
                time.sleep(sleep_time)
            self.last_send_time = time.time()


# --- Phone Number Normalization ---
def normalize_to_e164(phone_str: str) -> str:
    """
    Cleans phone strings and converts basic patterns to standard E.164.
    Fails intentionally if missing a leading '+' or country identification framework.
    """
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    
    if not cleaned:
        raise ValueError("Empty string or no valid digits found.")
        
    # Standard E.164 check: '+' followed by 7 to 15 digits
    if re.match(r'^\+[1-9]\d{6,14}$', cleaned):
        return cleaned
        
    # Attempt simple correction if user forgot the '+' but structured it with a country prefix
    if cleaned.isdigit() and len(cleaned) >= 10:
        logger.warning(f"Assuming missing '+' prefix for digits: {cleaned}")
        return f"+{cleaned}"
        
    raise ValueError(f"Number '{phone_str}' does not comply with E.164 requirements.")


# --- Worker Task ---
def process_single_sms(
    recipient: str, 
    sender: str, 
    template: str, 
    provider: SmsProvider, 
    rate_limiter: ThreadSafeRateLimiter,
    max_retries: int = 3
) -> Tuple[str, bool, str]:
    """Handles parsing, rate limiting, and delivery tracking for a single message."""
    try:
        normalized_recipient = normalize_to_e164(recipient)
    except ValueError as val_err:
        return recipient, False, f"Validation Error: {str(val_err)}"

    # Construct Template Placeholders
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_body = template.format(sender=sender, time=current_time, custom="")

    # Handle Rate Limiter Before Triggering
    rate_limiter.wait_if_needed()

    # Retry Strategy Execution
    base_delay = 1.5
    for attempt in range(max_retries + 1):
        try:
            provider.send_sms(to_number=normalized_recipient, from_number=sender, body=message_body)
            logger.info(f"Successfully sent SMS to {normalized_recipient}")
            return normalized_recipient, True, "Success"
        except Exception as error:
            if attempt < max_retries:
                sleep_duration = base_delay * (2 ** attempt)
                logger.warning(f"Transient failure sending to {normalized_recipient} (Attempt {attempt+1}/{max_retries+1}). Retrying in {sleep_duration}s... Error: {str(error)}")
                time.sleep(sleep_duration)
            else:
                logger.error(f"Failed to send SMS to {normalized_recipient} after {max_retries + 1} attempts.")
                return normalized_recipient, False, f"API Execution Failure: {str(error)}"

    return normalized_recipient, False, "Unknown processing timeout encountered."


# --- Core Logic Coordinator ---
def main():
    parser = argparse.ArgumentParser(description="Secure Production Ready Multi-threaded SMS Sender.")
    parser.add_argument('--sender', '-s', type=str, help="The sender mobile number (E.164 format)")
    parser.add_argument('--recipients-file', '-r', type=str, help="Path to text file containing target phone numbers")
    parser.add_argument('--recipients', type=str, help="Comma-separated inline list of recipient phone numbers")
    parser.add_argument('--message', '-m', type=str, default="Alert from {sender} at {time}", help="Message template.")
    parser.add_argument('--provider', type=str, default="twilio", choices=['twilio', 'vonage'], help="SMS gateway framework interface")
    parser.add_argument('--dry-run', action='store_true', help="Output operations locally without executing live API hooks")
    parser.add_argument('--concurrency', type=int, default=1, help="Total concurrent worker allocations allowed")
    parser.add_argument('--rate', type=float, default=1.0, help="Max outgoing message limits allocated per second")
    parser.add_argument('--test', action='store_true', help="Execute embedded testing harness framework validations")

    args = parser.parse_args()

    # Run internal diagnostics suite if explicitly called via CLI
    if args.test:
        run_internal_tests()
        sys.exit(0)

    # Resolve sender identifier requirements
    sender = args.sender
    if not sender and not args.dry_run:
        # Check environment as backup configurations fallback
        sender = os.getenv("TWILIO_FROM_NUMBER")
    if not sender:
        sender = input("Please enter your registered Sender Mobile Number (E.164 format): ").strip()
    
    try:
        sender = normalize_to_e164(sender)
    except ValueError as err:
        logger.critical(f"Invalid Sender Number Setup: {err}")
        sys.exit(1)

    # Build internal destination sets
    raw_recipients = []
    if args.recipients:
        raw_recipients.extend([item.strip() for item in args.recipients.split(",") if item.strip()])
    
    if args.recipients_file:
        if os.path.exists(args.recipients_file):
            with open(args.recipients_file, 'r') as file_obj:
                for line in file_obj:
                    line_clean = line.strip()
                    if line_clean and not line_clean.startswith("#"):
                        raw_recipients.append(line_clean)
        else:
            logger.critical(f"Target file path context missing: {args.recipients_file}")
            sys.exit(1)

    if not raw_recipients:
        logger.critical("Error: No recipient identifiers provided via pipeline arguments or text inputs.")
        sys.exit(1)

    # Initialize targeted network engine adapters
    if args.dry_run:
        provider_instance = DryRunProvider()
        logger.info("Initializing framework under isolated Dry-Run simulation engine conditions.")
    else:
        if args.provider.lower() == 'twilio':
            try:
                provider_instance = TwilioProvider()
            except Exception as init_err:
                logger.critical(f"Engine configuration exception context: {str(init_err)}")
                sys.exit(1)
        else:
            logger.critical(f"Provider engine context requested [{args.provider}] remains unimplemented in this version.")
            sys.exit(1)

    # Cost / Safety Advisory Message Context 
    if not args.dry_run:
        print("\n[IMPORTANT SAFETY NOTICE]")
        print("Executing this job will interface with external telecommunication networks and might incur financial costs.")
        print("Please ensure explicit structural recipient opt-in adherence before finalizing live broadcasts.")
        confirm = input("Do you wish to continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            logger.info("Broadcast execution aborted by supervisor interaction command.")
            sys.exit(0)

    # Initialize components
    rate_limiter = ThreadSafeRateLimiter(args.rate)
    
    successful_dispatches = 0
    failed_dispatches = []

    logger.info(f"Processing sequence initializing for {len(raw_recipients)} lines...")

    # Execute dynamic structural routing via Multi-threaded Executor pools
    max_workers = max(1, args.concurrency)
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="SmsWorker") as executor:
        futures = {
            executor.submit(
                process_single_sms, 
                recipient, 
                sender, 
                args.message, 
                provider_instance, 
                rate_limiter
            ): recipient for recipient in raw_recipients
        }
        
        for future in as_completed(futures):
            target_res, is_ok, log_msg = future.result()
            if is_ok:
                successful_dispatches += 1
            else:
                failed_dispatches.append((target_res, log_msg))

    # --- Print Job Summary Block Execution Summary ---
    print("\n" + "="*40)
    print("           BROADCAST SUMMARY            ")
    print("="*40)
    print(f"Total Evaluated Attempt Targets : {len(raw_recipients)}")
    print(f"Successful Dispatches           : {successful_dispatches}")
    print(f"Failed Delivery Records         : {len(failed_dispatches)}")
    print("="*40)

    if failed_dispatches:
        print("\nDetailed Exceptions Breakdown Logged:")
        for idx, (failed_num, error_desc) in enumerate(failed_dispatches, 1):
            print(f"  {idx}. Target Context: [{failed_num}] -> Resolution Reason: {error_desc}")
        print("="*40)
        sys.exit(1)
    else:
        print("All targets handled successfully with zero active exceptions returned.")
        sys.exit(0)


# --- Embedded Framework Unit Verification Suite ---
def run_internal_tests():
    """Runs a quick series of unit tests to verify normalization logic and dry-run execution."""
    logger.info("Executing embedded test framework...")
    
    # Test 1: Normalization Validation
    try:
        assert normalize_to_e164("+1 (415) 555-2671") == "+14155552671"
        assert normalize_to_e164("919876543210") == "+919876543210"
        logger.info("Test 1: Normalization parsing verified successfully.")
    except Exception as ex:
        logger.error(f"Test 1 Failure: {ex}")
        return

    # Test 2: Dry Run Single Delivery Run Loop
    try:
        provider = DryRunProvider()
        limiter = ThreadSafeRateLimiter(rate_per_sec=10)
        num, status, msg = process_single_sms(
            recipient="+14155552671", 
            sender="+1234567890", 
            template="Test message from {sender}", 
            provider=provider, 
            rate_limiter=limiter
        )
        assert status is True
        assert num == "+14155552671"
        logger.info("Test 2: Dry-run functional processing pipeline verified successfully.")
    except Exception as ex:
        logger.error(f"Test 2 Failure: {ex}")
        return

    logger.info("All internal checks executed successfully.")


if __name__ == '__main__':
    
    main()