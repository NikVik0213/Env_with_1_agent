from stable_baselines3.common.env_checker import check_env
from Search_start_Env import SearchEnv


env = SearchEnv()
# It will check your custom environment and output additional warnings if needed
check_env(env)