FROM ubuntu:16.04

RUN apt-get -y update 

RUN apt-get install -y openjdk-8-jre wget

RUN mkdir /opt/odl

RUN wget -O /opt/odl/odl.tar.gz https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/0.12.0/opendaylight-0.12.0.tar.gz

RUN tar -zxf /opt/odl/odl.tar.gz -C /opt/odl/

RUN mv /opt/odl/opendaylight* /opt/odl/magnesium

CMD /opt/odl/magnesium/bin/karaf

