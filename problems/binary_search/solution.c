#include <stdio.h>

int main(void) {
    int n, x;
    int a[1000];

    scanf("%d %d", &n, &x);
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    int left = 0;
    int right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (a[mid] == x) {
            printf("%d\n", mid);
            return 0;
        }
        if (a[mid] < x) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    printf("-1\n");
    return 0;
}
