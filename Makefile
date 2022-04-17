MININET = sudo mn

PYTHON = sudo python
PYTHON_OPTS =

# SWAT-S2 {{{1

swat-s2-init:
	git pull; cd examples/swat-s2/minicps/profinet_device; cmake -B build -S p-net; cmake --build build --target install; cd build; chmod +x set_network_parameters; cd ../../..

swat-s2-restart:
	cd examples/swat-s2; chmod +x ./restart.sh; ./restart.sh; cd ../..

swat-s2:
	cd examples/swat-s2; $(PYTHON) $(PYTHON_OPTS) run.py standard; cd ../..

swat-s2-dcp-tamp:
	cd examples/swat-s2; $(PYTHON) $(PYTHON_OPTS) run.py dcp_tampering; cd ../..

swat-s2-rpc-tamp:
	cd examples/swat-s2; $(PYTHON) $(PYTHON_OPTS) run.py rpc_tampering; cd ../..

swat-s2-dos:
	cd examples/swat-s2; $(PYTHON) $(PYTHON_OPTS) run.py dos; cd ../..
