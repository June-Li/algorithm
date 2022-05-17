def interval_index(value):
    if 0 < value <= 3000:
        return 0.03, 0
    elif 3000 < value <= 12000:
        return 0.1, 210
    elif 12000 < value <= 25000:
        return 0.2, 1410
    elif 25000 < value <= 35000:
        return 0.25, 2660
    elif 35000 < value <= 55000:
        return 0.3, 4410
    elif 55000 < value <= 80000:
        return 0.35, 7160
    elif 80000 < value:
        return 0.45, 15160
    else:
        return 0, 0


def cal_wage(wage):
    fund = wage * 0.23
    tax_basis = wage - fund - 5000
    prob, ded = interval_index(tax_basis)
    tax = tax_basis * prob - ded
    end_wag = wage - fund - tax
    return fund, tax_basis, tax, end_wag


def cal_fun():
    out_file = open('/Users/lijun/Downloads/salary.txt', 'w')
    for i in range(70):
        fund, tax_basis, tax, end_wag = cal_wage(i*1000)
        out_str = 'wage: ' + str(i*1000) + \
                  '   |   end_wag: ' + str(end_wag) + \
                  '   |   fund: ' + str(fund) + \
                  '   |   tax_basis: ' + str(tax_basis) + \
                  '   |   tax: ' + str(tax) + '\n'
        out_file.write(out_str)
        # print('fund: ', fund, '\ntax_basis: ', tax_basis, '\ntax: ', tax, '\nend_wag: ', end_wag)


if __name__ == '__main__':
    cal_fun()

