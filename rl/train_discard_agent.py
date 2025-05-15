import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv
from rl.crib_discard_env import CribDiscardEnv
import numpy as np
import os

def make_env():
    return CribDiscardEnv()

def main():
    # Create and wrap the environment
    env = DummyVecEnv([make_env])
    
    # Create evaluation environment
    eval_env = DummyVecEnv([make_env])
    
    # Create evaluation callback
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="models/",
        log_path="logs/",
        eval_freq=1000,  # More frequent evaluation for testing
        deterministic=True,
        render=False
    )
    
    # Initialize model with tuned hyperparameters
    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=1e-4,  # Increased learning rate
        buffer_size=50000,  # Smaller buffer
        learning_starts=5000,  # Fewer initial steps
        batch_size=64,  # Smaller batch size
        tau=1.0,  # Faster target network update
        gamma=0.99,  # Standard discount factor
        train_freq=4,  # More frequent training
        gradient_steps=1,  # Single gradient step
        target_update_interval=500,  # More frequent target updates
        exploration_fraction=0.1,  # Shorter exploration
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,  # Higher final epsilon
        max_grad_norm=10,  # Standard gradient clipping
        verbose=1
    )
    
    # Train the model with fewer timesteps
    total_timesteps = 50_000  # Reduced timesteps
    model.learn(
        total_timesteps=total_timesteps,
        callback=eval_callback,
        progress_bar=True
    )
    
    # Save the final model
    model.save("models/discard_dqn_agent_final")

if __name__ == "__main__":
    main()
