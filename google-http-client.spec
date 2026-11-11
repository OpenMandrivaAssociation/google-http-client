Name:		google-http-client
Version:	1.42.2
Release:	1
Summary:	Google HTTP client for Java
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/googleapis/google-http-java-client
# Tag v1.42.2. The archive has no prebuilt jars or class files.
Source0:	https://github.com/googleapis/google-http-java-client/archive/refs/tags/v%{version}.tar.gz#/google-http-client-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(org.apache.httpcomponents:httpclient)
BuildRequires:	mvn(org.apache.httpcomponents:httpcore)
BuildRequires:	mvn(commons-logging:commons-logging)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(com.google.guava:failureaccess)
BuildRequires:	mvn(com.google.j2objc:j2objc-annotations)
BuildRequires:	mvn(io.opencensus:opencensus-api)
BuildRequires:	mvn(io.opencensus:opencensus-contrib-http-util)
BuildRequires:	mvn(com.google.code.gson:gson)

%description
The Google HTTP client library %{version}: the core client, the Apache
HttpClient 4 transport, and the Gson JSON factory. Guava 33.6.0-jre is
class version 53, so these classes are Java 11. The library version
string is written into google-http-client.properties at build time.

%prep
%autosetup -n google-http-java-client-%{version}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
sed -i 's/${project.version}/%{version}/' google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties
grep -F -q 'google-http-client.version=%{version}' google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties

%build
set -eo pipefail
CP=%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/javax.annotation.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/j2objc-annotations.jar:%{_javadir}/opencensus-api.jar:%{_javadir}/opencensus-contrib-http-util.jar:%{_javadir}/gson-2.14.0.jar

find google-http-client/src/main/java -name '*.java' > core.list
test "$(wc -l < core.list)" -eq 157
mkdir -p core-classes
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d core-classes @core.list
mkdir -p core-classes/com/google/api/client/http
/bin/cp -f google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties core-classes/com/google/api/client/http/
cat > core.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client

EOF
jar cfm google-http-client.jar core.mf -C core-classes .
jar i google-http-client.jar
javap -verbose -cp google-http-client.jar com.google.api.client.http.HttpRequest | grep -F 'major version: 55'

find google-http-client-apache-v2/src/main/java -name '*.java' > v2.list
test "$(wc -l < v2.list)" -eq 6
mkdir -p v2-classes
javac --release 11 -encoding UTF-8 -Xlint:-options \
	-cp "google-http-client.jar:$CP" -d v2-classes @v2.list
cat > v2.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client.http.apache.v2

EOF
jar cfm google-http-client-apache-v2.jar v2.mf -C v2-classes .
jar i google-http-client-apache-v2.jar

find google-http-client-gson/src/main/java -name '*.java' > gson.list
test "$(wc -l < gson.list)" -eq 4
mkdir -p gson-classes
javac --release 11 -encoding UTF-8 -Xlint:-options \
	-cp "google-http-client.jar:$CP" -d gson-classes @gson.list
cat > gson.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client.json.gson

EOF
jar cfm google-http-client-gson.jar gson.mf -C gson-classes .
jar i google-http-client-gson.jar

cat > google-http-client.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client</artifactId>
  <version>1.42.2</version>
  <name>Google HTTP Client Library</name>
  <description>Google HTTP client for Java</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpclient</artifactId>
      <version>4.5.14</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
      <version>4.4.16</version>
    </dependency>
    <dependency>
      <groupId>com.google.code.findbugs</groupId>
      <artifactId>jsr305</artifactId>
      <version>3.0.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>33.6.0-jre</version>
    </dependency>
    <dependency>
      <groupId>com.google.j2objc</groupId>
      <artifactId>j2objc-annotations</artifactId>
      <version>3.1</version>
    </dependency>
    <dependency>
      <groupId>io.opencensus</groupId>
      <artifactId>opencensus-api</artifactId>
      <version>0.31.1</version>
    </dependency>
    <dependency>
      <groupId>io.opencensus</groupId>
      <artifactId>opencensus-contrib-http-util</artifactId>
      <version>0.31.1</version>
    </dependency>
  </dependencies>
</project>
EOF

cat > google-http-client-apache-v2.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client-apache-v2</artifactId>
  <version>1.42.2</version>
  <name>Apache HTTP transport for the Google HTTP Client</name>
  <description>Apache HttpClient 4 transport</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>com.google.http-client</groupId>
      <artifactId>google-http-client</artifactId>
      <version>1.42.2</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpclient</artifactId>
      <version>4.5.14</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
      <version>4.4.16</version>
    </dependency>
  </dependencies>
</project>
EOF

cat > google-http-client-gson.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client-gson</artifactId>
  <version>1.42.2</version>
  <name>Gson JSON factory for the Google HTTP Client</name>
  <description>Gson binding for the Google HTTP client</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>com.google.http-client</groupId>
      <artifactId>google-http-client</artifactId>
      <version>1.42.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.code.gson</groupId>
      <artifactId>gson</artifactId>
      <version>2.14.0</version>
    </dependency>
  </dependencies>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact google-http-client.pom:google-http-client.jar \
	--file-name google-http-client \
	--filelist .mfiles-core
sysjar install --buildroot %{buildroot} \
	--artifact google-http-client-apache-v2.pom:google-http-client-apache-v2.jar \
	--file-name google-http-client-apache-v2 \
	--filelist .mfiles-v2
sysjar install --buildroot %{buildroot} \
	--artifact google-http-client-gson.pom:google-http-client-gson.jar \
	--file-name google-http-client-gson \
	--filelist .mfiles-gson
awk '!seen[$0]++' .mfiles-core .mfiles-v2 .mfiles-gson > .mfiles

%check
set -eo pipefail
mkdir -p check
cat > check/Smoke.java << 'EOF'
import com.google.api.client.http.GenericUrl;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.apache.v2.ApacheHttpTransport;
import com.google.api.client.json.JsonParser;
import com.google.api.client.json.gson.GsonFactory;
public class Smoke {
	public static void main(String[] args) throws Exception {
		GenericUrl url = new GenericUrl("https://example.com/gradle");
		if (!"example.com".equals(url.getHost())) {
			throw new RuntimeException("host " + url.getHost());
		}
		if (!"1.42.2".equals(HttpRequest.VERSION)) {
			throw new RuntimeException("version " + HttpRequest.VERSION);
		}
		ApacheHttpTransport transport = new ApacheHttpTransport();
		if (transport.getHttpClient() == null) {
			throw new RuntimeException("no client");
		}
		JsonParser parser = GsonFactory.getDefaultInstance().createJsonParser("{\"k\":\"gradle\"}");
		parser.nextToken();
		parser.nextToken();
		String name = parser.getCurrentName();
		parser.nextToken();
		String text = parser.getText();
		parser.close();
		transport.shutdown();
		System.out.println("ghttp_ok " + HttpRequest.VERSION + " " + url.getRawPath() + " " + name + " " + text);
	}
}
EOF
CORE=%{buildroot}%{_javadir}/google-http-client.jar
V2=%{buildroot}%{_javadir}/google-http-client-apache-v2.jar
GSON=%{buildroot}%{_javadir}/google-http-client-gson.jar
test -f "$CORE"
test -f "$V2"
test -f "$GSON"
CP="$CORE:$V2:$GSON:%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar:%{_javadir}/javax.annotation.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/j2objc-annotations.jar:%{_javadir}/opencensus-api.jar:%{_javadir}/opencensus-contrib-http-util.jar:%{_javadir}/gson-2.14.0.jar"
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d check check/Smoke.java
java -cp "check:$CP" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'ghttp_ok 1.42.2 /gradle k gradle' check/out.txt

%files -f .mfiles
%doc LICENSE README.md
