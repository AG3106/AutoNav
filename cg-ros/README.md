# Concept-Graph
### Installation:

```bash
git clone https://github.com/IDEA-Research/Grounded-Segment-Anything/
cd Grounded-Segment-Anything/
git clone https://github.com/xinyu1205/recognize-anything
```
copy all the files in the recognize-anything folder to parent folder. (Grounded-Segment-Anything) <br>
copy the Dockerfile into the folder (Grounded-Segment-Anything) and build the image:
```bash
docker build -t gsa:v0 .
```
run the docker container:
```bash
docker run --gpus all -it --rm --net=host --privileged \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v "${PWD}":/home/appuser/Grounded-Segment-Anything \
	-e DISPLAY=$DISPLAY \
	--name=gsa \
	--ipc=host -it gsa:v0
```
add Replica dataset to `/home/appuser/Replica` <br>
```bash
export REPLICA_ROOT=/path/to/Replica # /home/appuser/Replica

export CG_FOLDER=/path/to/concept-graphs/ # /home/appuser/concept-graphs
export REPLICA_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/replica/replica.yaml
```
change the directories in config files in conceptgraph `/home/appuser/concept-graphs/conceptgraph/hydra_configs/`
<br>
change `base` to `base_detections` in `streamlined_detections.yaml`
