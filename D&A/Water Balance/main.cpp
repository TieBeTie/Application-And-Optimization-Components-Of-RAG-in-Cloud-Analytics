#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;

  vector<long long> sum;
  vector<int> len;

  for (int i = 0; i < n; ++i) {
    long long x;
    cin >> x;

    sum.push_back(x);
    len.push_back(1);

    while (sum.size() >= 2) {
      int k = sum.size();
      // если среднее предыдущего >= среднего последнего — сливаем
      if (sum[k - 2] * len[k - 1] >= sum[k - 1] * len[k - 2]) {
        sum[k - 2] += sum[k - 1];
        len[k - 2] += len[k - 1];
        sum.pop_back();
        len.pop_back();
      } else {
        break;
      }1
    }
  }

  cout << fixed << setprecision(9);
  for (int i = 0; i < (int)sum.size(); ++i) {
    double avg = (double)sum[i] / len[i];
    for (int j = 0; j < len[i]; ++j) {
      cout << avg << '\n';
    }
  }

  return 0;
}
