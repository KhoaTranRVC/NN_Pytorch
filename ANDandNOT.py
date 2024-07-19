# TODO: Set and_weight1, and_weight2, and and_bias
and_weight1 = 2.0
and_weight2 = 1.0
and_bias = -3.0

### Notebook grading

# Inputs and outputs (only 1 AND 1 should result in True)
and_test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
and_correct_outputs = [False, False, False, True]
and_outputs = []
# Generate output
for test_input in and_test_inputs:
    linear_combination = and_weight1 * test_input[0] \
                            + and_weight2 * test_input[1] \
                            + and_bias
    output = linear_combination >= 0
    and_outputs.append(output)

# Check output correctness
if and_outputs == and_correct_outputs:
    print('Nice!  You got it all correct.')
else:
    for index in range(len(and_outputs)):
        if and_outputs[index] != and_correct_outputs[index]:
            print("For the input {} your weights and bias \
produced an output of {}. The correct output is {}.".format(
                and_test_inputs[index],
                and_outputs[index],
                and_correct_outputs[index]
            ))
            break
