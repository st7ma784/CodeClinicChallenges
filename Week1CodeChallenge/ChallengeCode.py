# Sample list of results and whether the test was interesting
UsefulTest  = [True,False,True,False,True,True,False,False,True,True]

numbers = [11, 2, 3, 4, 5, 18, 7, 24, 30, 10]

# We want to find the useful tests where the results are Fizz,(divisible by  5) Buzz (divisible by 3) or FIZZBUZZ (divisible by 15)


# Filtering even numbers using a dictionary
fizz_count_dict = {}
buzz_count_dict = {}
fizzbuzz_count_dict = {}
for i in range(len(numbers)):
    number= numbers[i]
	if UsefulTest[i]:
		if number % 3 == 0:  # Check if the number is divisible by 3
			fizz_count_dict[number] = fizz_count_dict.get(number, 0) + 1
		if number % 5 == 0:
			buzz_count_dict[number] = buzz_count_dict.get(number, 0) + 1
		if number % 15 == 0:
			fizzbuzz_count_dict[number]  = fizzbuzz_count_dict.get(number, 0) + 1
fizz_numbers = list(fizz_count_dict.keys())
count_of_fizz = sum(fizz_count_dict.values())
buzz_numbers = list(buzz_count_dict.keys())
count_of_buzz = sum(buzz_count_dict.values())
fizzbuzz_numbers = list(fizzbuzz_count_dict.keys())
count_of_fizzbuzz = sum(fizzbuzz_count_dict.values())


print("There are {} Fizz numbers in the dictionary:".format(fizz_numbers))
print("There are {} Buzz numbers in the dictionary:".format(buzz_numbers))
print("There are {} FizzBuzz numbers in the dictionary:".format(fizzbuzz_numbers))
print("There are {} Fizz numbers in the results:".format(count_of_fizz))
print("There are {} Buzz numbers in the results:".format(count_of_buzz))
print("There are {} FizzBuzz numbers in the results:".format(count_of_fizzbuzz))
