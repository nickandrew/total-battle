#!/usr/bin/env python3
"""Calculate lifetime of essence in Omens tournament."""

import argparse

point_rates = [
    (979000, 48900),
    (490000, 24400),
    (163000, 16300),
    (19600, 7140),
    (0, 480),
]

def calc_lifespan(amount: int) -> int:
    amount_left = amount
    total_time = 0

    for a,b in point_rates:
        print(f'Considering {a=} {b=} {amount_left=} total time: {int(total_time)}')

        if amount_left > a:
            t = (amount_left - a) / b
            total_time += t
            amount_left = a

        if amount_left == 0:
            break

    return int(total_time)

def main():
    parser = argparse.ArgumentParser(description='Calculate essence lifetime')
    parser.add_argument('amt', type=int, help='Amount in chalice')
    args = parser.parse_args()

    print(calc_lifespan(args.amt))

if __name__ == '__main__':
    main()
