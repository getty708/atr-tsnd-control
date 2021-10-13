""" Initialize sensor nodes parameters.
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
    logger.info("== Sensor Data Recording ==")

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
    client.check_memory_status()
    
    # -- Start Recording --
    client.start_recording()
    client.start_event_listener()
    time.sleep(5)
    logger.debug("Recording Started (?)")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        # -- Stop Recording --
        logger.info("Stop Recording")
        client.stop_event_listener()
        client.stop_recording()
        
    # -- Check Memory Counts Again --
    time.sleep(10)
    client.check_memory_status()
    time.sleep(5)

    # == End ==
    client.terminate()
    logger.info("Success ... Connection closed.")


if __name__ == "__main__":
    main()
