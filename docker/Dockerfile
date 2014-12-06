FROM tjhei/deal-dev

MAINTAINER timo.heister@gmail.com

ENV HOME /root
WORKDIR $HOME

RUN git clone https://github.com/geodynamics/aspect.git

ADD script.sh $HOME/script.sh
CMD /root/script.sh




