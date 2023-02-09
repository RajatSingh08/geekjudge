#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin>>t;
    
    while (t--){
        int N;
        cin >> N;
        vector<int> nums(N);
        for(int i=0; i<N; i++)
            cin >> nums[i];

        int res=0;
        for(int i=0; i<N; i++)
            res^=nums[i];
        
        cout<<res<<endl;
    }
}