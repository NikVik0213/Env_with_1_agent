from stable_baselines3 import PPO
import os
from Search_start_Env import SearchEnv
import time



models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.isdir(models_dir):
	os.makedirs(models_dir)

if not os.path.isdir(logdir):
	os.makedirs(logdir)

env = SearchEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1,tensorboard_log = logdir)

timesteps = 6000
for i in range(50):
	print('Цикл обучения №',i)
	model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{timesteps*i}")