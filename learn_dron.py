from stable_baselines3 import PPO
import os
from Watering_start_Env import WateringEnv
import time



models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.isdir(models_dir):
	os.makedirs(models_dir)

if not os.path.isdir(logdir):
	os.makedirs(logdir)

env = WateringEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1,)

timesteps = 2000
for i in range(50):
	print('Цикл обучения №',i)
	model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{timesteps*i}")