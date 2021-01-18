// prints all primes < n, O(n^2)
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 2; i < n; i++) {
            boolean p = true;
            for (int j = 2; j < i; j++)
                if (i % j == 0)
                    p = false;
            if (p)
                System.out.println(i);
        }
    }
};