from stable_baselines3 import DQN
from rl.crib_discard_env import CribDiscardEnv

def main():
    env = CribDiscardEnv()
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100_000)
    model.save("models/discard_dqn_agent")

if __name__ == "__main__":
    main()
