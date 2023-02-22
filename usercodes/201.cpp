#include <bits/stdc++.h>
using namespace std;

int main()
{
    int t;
    cin >> t;
    while(t--)
    {
        int N, M, B;
        cin >> N >> M >> B;
    
        int Sx, Sy, Gx, Gy;
        vector<vector<char>> mat(N, vector<char>(M));
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < M; j++)
            {
                cin >> mat[i][j];
                if (mat[i][j] == 'S')
                    Sx = i, Sy = j;
                else if (mat[i][j] == 'G')
                    Gx = i, Gy = j;
            }
        }
    
        queue<array<int, 3>> Q;
        vector<vector<vector<int>>> dist(N, vector<vector<int>>(M, vector<int>(B + 1, 1e9)));
    
        Q.push({Sx, Sy, B});
        dist[Sx][Sy][B] = 0;
    
        int dx[] = {0, -1, 0, 1};
        int dy[] = {1, 0, -1, 0};
    
        while (!Q.empty())
        {
            int x = Q.front()[0];
            int y = Q.front()[1];
            int bomb = Q.front()[2];
            Q.pop();
    
            for (int i = 0; i < 4; i++)
            {
                int nx = x + dx[i];
                int ny = y + dy[i];
    
                if (nx < 0 || nx >= N || ny < 0 || ny >= M)
                    continue;
    
                if (mat[nx][ny] == '#' && bomb > 0 && dist[nx][ny][bomb] == 1e9)
                {
                    dist[nx][ny][bomb - 1] = dist[x][y][bomb] + 1;
                    Q.push({nx, ny, bomb - 1});
                }
                else if (mat[nx][ny] != '#' && dist[nx][ny][bomb] == 1e9)
                {
                    dist[nx][ny][bomb] = dist[x][y][bomb] + 1;
                    Q.push({nx, ny, bomb});
                }
            }
        }
    
        int ans = *min_element(dist[Gx][Gy].begin(), dist[Gx][Gy].end());
        if (ans == 1e9)
            ans = -1;
        cout << ans << "\n";
    }
    return 0;
}