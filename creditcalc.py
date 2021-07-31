import argparse
import math
import sys

parse = argparse.ArgumentParser(description="Loan Calculator")
parse.add_argument("--type", choices=["annuity", "diff"])
parse.add_argument("--payment", type=float)

parse.add_argument("-p", "--principal", type=float)
parse.add_argument("-n", "--periods", type=int)
parse.add_argument("-i", "--interest", type=float)

args = parse.parse_args()
isStart = True


def error():
    global isStart
    print("Incorrect parameters.")
    isStart = False


if len(sys.argv) < 5:
    error()
elif args.type != "annuity" and args.type != "diff":
    error()
elif args.type == "diff" and args.payment:
    error()
else:
    my_list = [args.payment, args.principal, args.periods, args.interest]
    for item in my_list:
        if item:
            if item < 0:
                error()

if isStart:
    if args.type == "annuity":

        def calc_payment():
            p = args.principal
            n = args.periods
            i = args.interest / (12 * 100)

            ordinary_annuity = math.ceil(p * ((i * ((1 + i) ** n)) / ((1 + i) ** n - 1)))
            overpayment = math.ceil(ordinary_annuity * n - p)
            print(f"Your annuity payment = {str(ordinary_annuity)}!\n"
                  f"Overpayment = {overpayment}")

        def calc_principle():
            ordinary_annuity = args.payment
            n = args.periods
            i = args.interest / (12 * 100)

            principle = math.floor(ordinary_annuity / (i * (1 + i) ** n / ((1 + i) ** n - 1)))
            overpayment = math.ceil(ordinary_annuity * n - principle)
            print(f"Your loan principal = {principle}!\n"
                  f"Overpayment = {overpayment}")

        def calc_periods():
            p = args.principal
            ordinary_annuity = args.payment
            i = args.interest / (12 * 100)

            periods = math.ceil(math.log((ordinary_annuity / (ordinary_annuity - i * p)), 1 + i))
            overpayment = math.ceil(ordinary_annuity * periods - p)

            if periods >= 12:
                periods_format = (str(periods // 12) + (" years" if periods >= 24 else " year")
                                  + ((" " + str(periods % 12) + (" months" if periods % 12 >= 2 else " month"))
                                     if periods % 12 > 1 else ""))
            else:
                periods_format = str(periods) + (" months" if periods % 12 >= 2 else " month")
            print(f"It will take {periods_format} to repay this loan!\n"
                  f"Overpayment = {overpayment}")


        if not args.principal:
            calc_principle()
        if not args.periods:
            calc_periods()
        if not args.payment:
            calc_payment()

    elif args.type == "diff":

        def calc_diff():
            p = args.principal
            n = args.periods
            i = args.interest / (12 * 100)

            current_month = 1
            overpayment = -p
            while current_month <= n:
                d = p / n + i * (p - (p * (current_month - 1)) / n)
                overpayment += math.ceil(d)
                print(f"Month {current_month}: payment is {math.ceil(d)}")
                current_month += 1
            print(f"\nOverpayment = {math.ceil(overpayment)}")


        calc_diff()
