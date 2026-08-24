#include<iostream>
#include<vector>
using namespace std;

void printvector(const vector<int> &v){
    for(int i=0;i<v.size;i++){
        cout<<v.at(i)<<endl;
    }
}
int main(){
vector<int> nums={1,2,4}
printvector(nums);

}