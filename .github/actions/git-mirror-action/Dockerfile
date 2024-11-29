FROM alpine

RUN apk add --no-cache git git-lfs openssh-client

ADD *.sh /

#RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash

ENTRYPOINT ["/entrypoint.sh"]
