# depend-o-nator make file

python_cmd=python
ifeq ($(OS),Windows_NT)
python_cmd=py.exe
endif

.DEFAULT: help
.PHONY: all test run 


help:
	@echo "depend-o-nator"
	@echo ""
	@echo "[Execute]"    
	@echo "  run              | run the script"
	@echo "  test             | run the script, dont graph just debug"
	@echo "  graph            | makes the graph"
	@echo "  pull             | pull graph related docker images"
	@echo "  run-images       | run the docker images for graphing"
	
	
	
	@echo ""
	

test:
	@$(python_cmd) -m depend-o-nator.main --test


run:
	@$(python_cmd) -m depend-o-nator.main >depend-o-nator.dot

pull:
	@docker pull yuzutech/kroki-mermaid
	@docker pull yuzutech/kroki-blockdiag
	@docker pull yuzutech/kroki

run-images:
	@docker-compose up -d
	
graph: 
	@wget "http://localhost:8000/blockdiag/svg/$(shell cat depend-o-nator.dot | python encode.py)"  -O graph.svg
