""" Initialize sensor nodes parameters.
"""
from tsndctl.device import TSND151
import time
from logging import getLogger
import hydra
from omegaconf import DictConfig, OmegaConf

logger = getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    logger.info("== Initialize Sensor Node Parameters ==")

    # -- Initialize client object --
    client = TSND151(cfg.client.name, cfg.client.port, timeout=cfg.timeout)
    time.sleep(5)
    logger.debug("Success ... Initialize TSND151() object and open connection.")
    
    # -- Update Senor Parameters --
    client.init_device()
    time.sleep(5)
    logger.info("Success ... Parameters are updated!")

    # -- End --
    client.terminate()
    logger.info("Success ... Connection closed.")


if __name__ == "__main__":
    main()
