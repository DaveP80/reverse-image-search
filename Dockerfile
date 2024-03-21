FROM public.ecr.aws/lambda/python@sha256:1d922f123370801843aad18d0911759c55402af4d0dddb601181df4ed42b2ce2 as build
RUN dnf install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:1d922f123370801843aad18d0911759c55402af4d0dddb601181df4ed42b2ce2
RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm
RUN pip install attrs==23.2.0
RUN pip install boto3==1.34.64
RUN pip install botocore==1.34.64
RUN pip install certifi==2024.2.2
RUN pip install charset-normalizer==3.3.2
RUN pip install h11==0.14.0
RUN pip install idna==3.6
RUN pip install jmespath==1.0.1
RUN pip install outcome==1.3.0.post0
RUN pip install packaging==24.0
RUN pip install PySocks==1.7.1
RUN pip install python-dateutil==2.9.0.post0
RUN pip install python-dotenv==1.0.1
RUN pip install requests==2.31.0
RUN pip install selenium==4.18.1
RUN pip install s3transfer==0.10.1
RUN pip install six==1.16.0
RUN pip install sniffio==1.3.1
RUN pip install sortedcontainers==2.4.0
RUN pip install trio==0.24.0
RUN pip install trio-websocket==0.11.1
RUN pip install typing_extensions==4.10.0
RUN pip install typing_extensions==4.10.0
RUN pip install urllib3==2.2.1
RUN pip install webdriver-manager==4.0.1
RUN pip install wsproto==1.2.0
COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/
COPY lambda_function.py ./
CMD [ "lambda_function.lambda_handler" ]
