# Welcome To UFM NDT Plugin

To deploy the plugin on UFM Appliance, you should:
-	go to UFM Appliance machine (for me it’s r-ufm235, set up by Avi);
-	run _en_ (short for enable);
-	run _co t_ (short for config terminal);
-	run _image fetch scp://<user>:<password>@<host>/auto/mtrswgwork/atolikin/ndt_testing/ufm-plugin-ndt.tar.gz_ – fetch the image from the machine that has access to /auto share, I used my virtual machine with default root credentials;
-	load the image with _docker load ufm-plugin-ndt.tar.gz_;
-	run _ufm plugin ndt add_;
-	check that plugin is up and running with show _docker ps_;

To deploy the plugin with UFM (SA or HA), you should:
-	install the latest version of UFM;
-	load the image with _sudo docker load -i /auto/mtrswgwork/atolikin/ndt_testing/ufm-plugin-ndt.tar.gz_;
-	run _/opt/ufm/scripts/manage_ufm_plugins.py add -p ndt_;
-	check that plugin is up and running with _docker ps_;

Log file ndt.log is located in /opt/ufm/files/log on host.

-----------------------------------------------------------------------------------------------------------
  
Example of a test scenario (positive flow):
-	run UFM simulation based on /auto/mtrswgwork/atolikin/ndt_testing/ibnetdiscover_director.txt file;
-	_curl -k -i -X POST -H "Content-Type:application/json" -d ‘<request>’ ‘http://<host_ip>/ufmRest<V2><V3>/plugin/ndt/upload_metadata’_: upload the data (ndts can be found here: /auto/mtrswgwork/atolikin/ndt_testing/<name>.ndt), don’t forget to replace Windows line endings with Linux ones;
-	_curl -k -i -X GET 'http:// <host_ip>/ ufmRest<V2><V3>/plugin/ndt/list'_: check a list of uploaded NDTs;
-	_curl -k -i -X POST -H "Content-Type:application/json" -d ‘’ 'http://<host_ip>/ ufmRest<V2><V3>/plugin/ndt/compare’_: run topology comparison;
-	_curl -k -i -X GET 'http:// <host_ip>/ ufmRest<V2><V3>/plugin/ndt/reports’_: check a list of reports;
-	_curl -k -i -X GET 'http:// <host_ip>/ ufmRest<V2><V3>/plugin/ndt/reports/1’_: check the content of the 1-st (and the only one) report;
-	_curl -k -i -X POST -H "Content-Type:application/json" -d ‘<request>’ 'http://<host_ip>/ ufmRest<V2><V3>/plugin/ndt/compare’_: run topology periodic comparison, e.g., startTime is current time, endTime is current time + 2 minutes, interval is 1 minute;
-	wait for 3 minutes and run _curl -k -i -X GET 'http://<host_ip>/ ufmRest<V2><V3>/plugin/ndt/reports’_ to check the list of reports again – there should be 4 now.
-	_curl -k -i -X POST -H "Content-Type:application/json" -d ‘’ 'http://<host_ip>/ ufmRest<V2><V3>/plugin/ndt/delete’_: delete NDTs;