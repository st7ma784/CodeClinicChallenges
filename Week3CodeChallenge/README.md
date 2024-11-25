# Week 3 Code Challenge: Summing Tables Together

## Objective
The goal of this challenge is to sum tables together around a single column as a primary key.

## Task Outline

### 1. Understand the Problem
- Find the data.csv file in the repository.
- Identify the columns to be summed, and the primary key column.

### 2. Input Data
- Describe the format of the input tables.
- Provide example tables.

### 3. Output Data
- Define the format of the output table.
- Provide an example of the expected result.

### 4. Algorithm Design
- Outline the steps to sum the tables.
- Consider edge cases (e.g., missing keys, different table sizes).
- Consider how to iterate over an unknown number of tables
- consider if there are external libraries like pandas, numpy or torch that might simplify the task (loading them will be timed!)

### 5. Implementation
- (re)Write the code to sum the tables as sum_tables_on_key function.
- Ensure the code handles edge cases.
- Test the implementation.

### 6. Testing
- Create test cases to validate the implementation.
- Include tests for edge cases.

## Example

### Input Tables
| ID | Value1 | Value2 |
|----|--------|--------|
| 1  | 10     | 20     |
| 2  | 30     | 40     |

| ID | Value1 | Value2 |
|----|--------|--------|
| 1  | 5      | 15     |
| 3  | 25     | 35     |

### Output Table
| ID | Value1 | Value2 |
|----|--------|--------|
| 1  | 15     | 35     |
| 2  | 30     | 40     |
| 3  | 25     | 35     |

## Notes
- Ensure the primary key column is unique in the output table.
- Handle cases where a key is present in one table but not the other.
