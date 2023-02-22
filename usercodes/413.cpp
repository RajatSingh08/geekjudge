#include <bits/stdc++.h>
using namespace std;
struct node{
    long long mx,tmx,sum;
};
long long inf=(long long)1e16+77;
int main()
{
    int t;cin>>t;
    while(t--){
        long long n,m;cin>>n>>m;
        vector<vector<pair<long long,long long>>> g(n+1);
        for(int i=0;i<m;i++){
            long long a,b,c;cin>>a>>b>>c;
            g[a].push_back({b,c});
            g[b].push_back({a,c});
        }
        set<pair<long long,long long>> s;
        vector<node> v(n+1,{0,inf,inf});
        v[1]={0,0,0};
        for(int i=1;i<=n;i++){
            s.insert({inf,i});
        }
        s.erase({inf,1});
        s.insert({0,1});
        while(s.size()){
            auto it=s.begin();
            long long p=(*it).second;
            long long e=(*it).first;
            for(auto itt:g[(*it).second]){
                long long c=itt.first;
                if(v[p].sum+itt.second<v[c].sum){
                    s.erase({v[c].sum,c});
                    v[c].sum=v[p].sum+itt.second;
                    s.insert({v[c].sum,c});
                }
                long long a=v[p].tmx+itt.second-max(itt.second,v[p].mx)+max(itt.second,v[p].mx)/2;
                long long b=v[c].tmx-v[c].mx+v[c].mx/2;
                if(a<b){
                    v[c].tmx=v[p].tmx+itt.second;
                    v[c].mx=max(v[p].mx,itt.second);
                }
                b=v[c].tmx-v[c].mx+v[c].mx/2;
                a=v[p].sum+itt.second/2;
                if(a<b){
                    v[c].tmx=v[p].sum+itt.second;
                    v[c].mx=itt.second;
                }
            }
            s.erase(it);    
        }
        cout<<v[n].tmx-v[n].mx+v[n].mx/2<<endl;
    }
}