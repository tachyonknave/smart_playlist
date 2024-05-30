import yaml


class Config:
    def __init__(self):
        self.config_dict = dict()

    def load_config(self):
        with open('./config/config.yaml', 'r') as config_file:
            self.config_dict = yaml.safe_load(config_file)

    def get_channel_list(self):
        return self.config_dict['source_playlist_names']

    def get_target_playlist(self):
        return self.config_dict['target_playlist_id']

    def get_sleep_time(self):
        return self.config_dict['sleep_seconds']
