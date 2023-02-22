#include<bits/stdc++.h>
using namespace std;
int main(){
    int t;cin>>t;
    while(t--){
        int n,m;cin>>n>>m;
        vector<vector<int>> g(n+1);
        while(m--){
            int a,b;cin>>a>>b;
            g[a].push_back(b);
            g[b].push_back(a);
        }
        vector<int> d(n+1,0),q,vis(n+1,0),ans;
        q.push_back(1);
        for(int i=0;i<q.size();i++){
            vis[q[i]]=1;
            for(auto it:g[q[i]]){
                if(!vis[it]){
                    d[it]=d[q[i]]+1;
                    q.push_back(it);
                }
            }
        }
        if(d[n]){
            q.clear();
            q.push_back(n);   
            for(int j=d[n];j>=0;j--){
                vector<int> tmp;
                for(int i=0;i<q.size();i++){
                    ans.push_back(q[i]);
                    for(auto it:g[q[i]]){
                        if(d[it]==j-1){
                            tmp.push_back(it);
                            d[it]=INT_MAX;
                        }
                    }
                }
                q=tmp;
            }
            sort(ans.begin(),ans.end());
            for(auto it:ans){
                cout<<it<<" ";
            }
            cout<<endl;
        }else{cout<<-1<<endl;}
    }
}