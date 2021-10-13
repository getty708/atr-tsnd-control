""" Download Data in Device's Memory.
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
    logger.info("== Download Data in Device's Memory ==")

    # == Initialize client object ==
    client = TSND151(
        cfg.client.name, cfg.client.port,
        timeout=cfg.timeout,
        # logger=getLogger(f"tsndctl.TSND151.{cfg.client.name}"),
    )
    time.sleep(5)
    logger.debug("Success ... Initialize TSND151() object and open connection.")
    
    # == Sensor Data Recoring ==
    # -- Check Memory Counts --
    outputs = client.check_memory_status()
    time.sleep(5)
    num_entry = outputs["MemEntryCount"]["num_entry"]
    
    # -- Download --
    # client.start_recording()
    for i in range(num_entry):
        print(f"[{i+1:>2}/{num_entry:>2}] Do you want to download entry {i+1}? [Y/n] >> ")
        choice = input()
        if choice == "Y":
            client.read_mem_data(i+1)
            time.sleep(2)

    # == End ==
    client.terminate()
    logger.info("Success ... Connection closed.")


if __name__ == "__main__":
    main()
