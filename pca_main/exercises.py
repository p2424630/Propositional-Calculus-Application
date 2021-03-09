# @Author: GKarseras
# @Date:   22 Feb 17:10

# class Exercise:
#
#     def __init__(self, prop, question):
#         self.prop = prop
#         self.question = question
#
#
# class DeMorgan(Exercise):
#     pass


de_morgan = [
    {
        'prop': 'Q or P',
        'question': f'Apply De Morgan law to the following proposition: Q or P'
    },
    {
        'prop': 'Q or (P or R)',
        'question': "Apply De Morgan's law to the following proposition: Q or (P or R)"
    }
]

asos = [
    {
        'prop': 'E or Z',
        'question': f'proposition: E or Z'
    },
    {
        'prop': 'E or Z iff E',
        'question': "proposition: E or Z iff E"
    }
]

exer = {
    'de_morgan': de_morgan,
    'asos': asos
}
