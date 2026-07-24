import asyncio,aiohttp


url='https://jsonplaceholder.typicode.com/posts'
# url='https://reqres.in/api/users/2'

async def fetchin():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            data=await response.json()
            print(data)
            
asyncio.run(fetchin())

# async def demo():
#     # s= await asyncio.slee
#     s='amit'
#     return s
# async def mmmm():
#     result =await demo()cls

#     print(result)

# asyncio.run(mmmm())   # ye coroutine object hai, actual "Hello" nahi
