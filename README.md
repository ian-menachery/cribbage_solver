# Cribbage RL Project

## Overview
This project implements a reinforcement learning (RL) agent to play the card game Cribbage. The agent is trained using a Deep Q-Network (DQN) and competes against a value-based bot.

## Purpose
The goal is to explore how RL can be applied to card games, specifically Cribbage, and to develop an agent that can learn and improve its strategy over time.

## Methods
- **Environment**: A custom Gym environment (`CribDiscardEnv`) simulates the Cribbage game, handling card dealing, scoring, and opponent simulation.
- **RL Agent**: A DQN agent is trained to make discard decisions based on the current hand and game state.
- **Training**: The agent is trained using the `train_discard_agent.py` script, which uses the Stable Baselines3 library.
- **Evaluation**: The agent's performance is evaluated against a value-based bot using the `rl_vs_random_match.py` script.

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the RL Agent**:
   ```bash
   python rl/train_discard_agent.py
   ```

3. **Run the Match**:
   ```bash
   python scripts/rl_vs_random_match.py
   ```

## Results
The RL agent achieves a win rate of approximately 40% against the value-based bot, demonstrating significant improvement over initial versions.

## Future Work
- Experiment with different RL algorithms (e.g., PPO).
- Further tune hyperparameters and reward shaping.
- Extend the agent to handle more complex game scenarios.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 