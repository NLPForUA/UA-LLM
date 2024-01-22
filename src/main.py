import hydra
import omegaconf


@hydra.main(config_path="configs")
def my_app(cfg: omegaconf.DictConfig) -> None:
    task = hydra.utils.instantiate(cfg.task, _recursive_=True)
    task.run()


if __name__ == "__main__":
    my_app()
