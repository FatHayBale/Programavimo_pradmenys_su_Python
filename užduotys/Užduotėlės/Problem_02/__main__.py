import json
import test

def main():
    with open('Cases.json', 'r') as f:
        data = json.load(f)
        cases = data['cases']

    for idx, case in enumerate(cases):
        inputs = case['input']
        expected_answer = case['answer']

        result = test.run(*inputs)

        if result == expected_answer:
            print(f"Test case {idx+1}: Passed")
        else:
            print(f"Test case {idx+1}: Failed (Expected: {expected_answer}, Got: {result})")

if __name__ == '__main__':
    main()
