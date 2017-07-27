import torch
import time
from termcolor import colored as clr
from utils import not_implemented


class BaseAgent(object):
    def __init__(self, action_space):
        self.actions = action_space
        self.action_no = self.actions.n

        self.step_cnt = 0
        self.ep_cnt = 0
        self.ep_reward_cnt = 0
        self.ep_reward = []
        self.max_mean_rw = -100

    def evaluate_policy(self, obs):
        not_implemented(self)

    def improve_policy(self, _state, _action, reward, state, done):
        not_implemented(self)

    def gather_stats(self, reward, done):
        self.step_cnt += 1
        self.ep_reward_cnt += reward
        if done:
            self.ep_cnt += 1
            self.ep_reward.append(self.ep_reward_cnt)
            self.ep_reward_cnt = 0

    def display_setup(self, env, config):
        print("----------------------------")
        print("Agent        : %s" % self.name)
        print("Seed         : %d" % config.seed)
        print("--------- Training ----------")
        print("Hidden Size  : %d" % config.agent.hidden_size)
        print("Batch        : %d" % config.agent.batch_size)
        print("Slow Lr      : %.6f" % config.agent.lr)
        print("-----------------------------")
        print("stp, nst, act  |  return")
        print("-----------------------------")

    def display_stats(self, start_time):
        mean_rw = torch.FloatTensor([self.ep_reward]).mean()
        fps = self.step_cnt / (time.time() - start_time)

        max_mean_rw = self.max_mean_rw
        bg_color = 'on_cyan'
        bg_color = 'on_magenta' if mean_rw > max_mean_rw else bg_color
        self.max_mean_rw = mean_rw if mean_rw > max_mean_rw else max_mean_rw

        print(clr("[%s] step=%7d, rw/ep=%3.2f, fps=%.2f, @=%4d eps."
              % (self.name, self.step_cnt, mean_rw, fps, len(self.ep_reward)),
              'white', bg_color))
        self.ep_reward.clear()

    def display_final_report(self, ep_cnt, step_cnt, elapsed_time):
        fps = step_cnt / elapsed_time
        print(clr("[  %s   ] finished after %d eps, %d steps."
              % ("Main", ep_cnt, step_cnt), 'white', 'on_magenta'))
        print(clr("[  %s   ] finished after %.2fs, %.2ffps."
              % ("Main", elapsed_time, fps), 'white', 'on_magenta'))

    def display_model_stats(self):
        pass