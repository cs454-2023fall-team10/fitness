# global settings

# model_name : 사용할 model을 결정합니다 (sentence_bert, openai)
model_name = "sentence_bert"

# DISTANCE_THRESHOLD : 허용할 수 있는 distance_threshold의 최댓값.
# ex) DISTANCE_THRESHOLD = 0 : similarity_threshold 신경 안씀
#     DISTANCE_THRESHOLD = 1 : 마지막으로 도달한 node의 설명이 intent와 똑같아야 함.
DISTANCE_THRESHOLD = 0.1

# alpha: user_fitness와 admin_fitness간의 비율, alpha가 늘어날수록 user_fitness의 반영비율 증가
alpha = 0.6

# intent_file_path : GPT가 생성한 user intent들이 담겨있는 파일의 경로.
intent_file_path = "./chatbot-dataset/intents/gpt-4-1106-preview/jobs-homepage"


def get_similarity_threshold(DEPTH_THRESHOLD, DISTANCE_THRESHOLD, current_depth) :
    # current_depth에 따른 choice들의 distance_threshold를 어떻게 설정할 것인지 결정합니다.
    # ex) return (DISTANCE_THRESHOLD / DEPTH_THRESHOLD) * current_depth
    #   => 0부터 시작하여 DISTANCE_THRESHOLD까지 linear하게 증가

    return (DISTANCE_THRESHOLD / DEPTH_THRESHOLD) * current_depth * (1/2)

def get_user_fitness(DEPTH_THRESHOLD, DISTANCE_THRESHOLD, path_length, final_similarity, penalty) :
    # 최종적으로 user_fitness를 어떻게 계산할지 결정합니다.
    # path_length : user가 이동한 거리 ex) A -> B -> A -> C = 4
    # final_similarity : user가 최종적으로 도달한 node와 user의 indent간 similarity
    # penalty : similarity_penalty와 depth_penalty를 모두 더한 값

    return (DEPTH_THRESHOLD - path_length) + (final_similarity - DISTANCE_THRESHOLD) - penalty

def similarity_penalty(choice_similarities, similarity_threshold) :
    # 특정 node에서 모든 choice들이 similarity_threshold를 넘지 못하였을 때, 얼마만큼의 penalty를 줄지 결정합니다.
    # penalty를 얼마나 줄지 결정하는 것이기에, positive value를 주어야 합니다.
    # choice_similarities : 특정 node의 모든 choice들의 similarity 값 모음
    # similarity_threshold : choice들이 넘어야 했던 threshold 값

    return (similarity_threshold) * len(choice_similarities) - sum(choice_similarities)

def depth_penalty(DEPTH_THRESHOLD) :
    # depth_threshold를 넘은 user에 대해 fitness값을 어떻게 부여할지 설정합니다.
    # penalty를 얼마나 줄지 결정하는 것이기에, positive value를 주어야 합니다.

    return DEPTH_THRESHOLD