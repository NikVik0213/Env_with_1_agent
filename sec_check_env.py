from Search_start_Env import SearchEnv


env = SearchEnv()
episodes = 50

for episode in range(episodes):
	done = False
	obs = env.reset()
	while True:#not done:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward,truncated, done, info = env.step(random_action)
		print('reward',reward)