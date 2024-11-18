# Possible Grades Solver

Calculate what grades you need on your remaining assignments to get certain final grades

## Dependencies 
scipy

## Usage
`python main.py <grades>`

The grades file contains json data with the grade and threshold data

### Minimal example grades file
```json
{
    "thresholds":{
        "A":90.0
    },
    "grades":{
        "Homework": {
            "grade": 80.0,
            "weight": 60.0
        },
        "Exam":{
            "grade": -1,
            "weight": 40.0
        }
    }
}
```

This will evaluate the minimum grade needed for the Exam to get a final grade of A (90%)