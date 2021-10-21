""" Clear Memory
"""
from tsndctl.device import TSND151
import time
import hydra
from omegaconf import DictConfig, OmegaConf
from logging import getLogger

logger = getLogger(__name__)


@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    logger.info("== Check & Clear Memory ==")
    
    # -- Initialize client object --
    client = TSND151(cfg.client.name, cfg.client.port, timeout=cfg.timeout)
    time.sleep(5)
    logger.debug("Success ... Initialize TSND151() object and open connection.")
    
    # -- Check Memory Counts --
    outputs = client.check_memory_status()
    time.sleep(5)
    # num_entry = outputs["MemEntryCount"]["num_entry"]
    
    # -- Check Device Paramters --
    client.get_device_status()
    time.sleep(5)
    
    # -- End --
    client.terminate()
    logger.info("Success ... Connection closed.")


if __name__ == "__main__":
    main()
