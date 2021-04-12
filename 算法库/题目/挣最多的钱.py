state_transition_table = {}
state_value_table = {}
route_list_tables = []


def work_operator(work_list, state_transition_table, state_value_table, opt_index):
    if opt_index == 0:
        return work_list[opt_index][2]

    if state_transition_table[opt_index] == None:
        v_1 = work_list[opt_index][2]
    elif state_value_table[state_transition_table[opt_index]] == None:
        v_1 = work_list[opt_index][2] + work_operator(work_list, state_transition_table, state_value_table,
                                                      state_transition_table[opt_index])
    else:
        v_1 = work_list[opt_index][2] + state_value_table[state_transition_table[opt_index]]

    if state_transition_table[opt_index - 1] == None:
        v_2 = work_list[opt_index - 1][2]
    elif state_value_table[state_transition_table[opt_index - 1]] == None:
        v_2 = work_operator(work_list, state_transition_table, state_value_table, opt_index - 1)
    else:
        v_2 = state_value_table[state_transition_table[opt_index - 1]]

    # if v_1 > v_2:
    #     max_money = v_1
    # else:
    #     max_money = v_2
    max_money = max(v_1, v_2)
    state_value_table[opt_index] = max_money
    return max_money


def main():
    work_list = [[1, 4, 5], [3, 5, 1], [0, 6, 8], [4, 7, 4], [3, 8, 6], [5, 9, 3], [6, 10, 2], [8, 11, 4]]
    # work_list = [[1, 3, 1], [1, 5, 1], [5, 7, 1]]

    for index_one in range(len(work_list) - 1, -1, -1):
        state_value_table[index_one] = None
        for index_two in range(len(work_list) - 1, -1, -1):
            if index_two >= index_one:
                continue
            if work_list[index_one][0] >= work_list[index_two][1]:
                state_transition_table[index_one] = index_two
                break
        if index_one not in state_transition_table.keys():
            state_transition_table[index_one] = None

    max_money = work_operator(work_list, state_transition_table, state_value_table, len(work_list) - 1)
    print(max_money)
    # print(route_list_tables)

    # print(state_transition_table)
    # print(state_value_table)


if __name__ == '__main__':
    main()
