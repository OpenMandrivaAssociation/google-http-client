Name:		google-http-client
Version:	2.2.0
Release:	1
Summary:	Google HTTP client for Java
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/googleapis/google-http-java-client
# Tag v2.2.0. The archive has no prebuilt jars or class files.
Source0:	https://github.com/googleapis/google-http-java-client/archive/refs/tags/v%{version}.tar.gz#/google-http-client-%{version}.tar.gz
# Gradle pins all three artifacts at 1.42.2.
Source1:	https://github.com/googleapis/google-http-java-client/archive/refs/tags/v1.42.2.tar.gz#/google-http-client-1.42.2.tar.gz

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
BuildRequires:	mvn(com.google.errorprone:error_prone_annotations)

%description
The Google HTTP client library %{version}: the core client, the Apache
HttpClient 4 transport, and the Gson JSON factory. The 1.42.2 jars stay
installed beside them. Guava is class version 53, so these classes are
Java 11. The library version string is written into
google-http-client.properties at build time.

%prep
%autosetup -n google-http-java-client-%{version}
tar -xf %{SOURCE1}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
sed -i 's/${project.version}/%{version}/' google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties
grep -F -q 'google-http-client.version=%{version}' google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties
sed -i 's/${project.version}/1.42.2/' google-http-java-client-1.42.2/google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties
grep -F -q 'google-http-client.version=1.42.2' google-http-java-client-1.42.2/google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties

%build
set -eo pipefail
CP=%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/javax.annotation.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/j2objc-annotations.jar:%{_javadir}/opencensus-api.jar:%{_javadir}/opencensus-contrib-http-util.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/error_prone_annotations.jar

write_poms() {
	ver="$1"
	dest="$2"
	cat > "$dest/google-http-client.pom" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client</artifactId>
  <version>$ver</version>
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
	cat > "$dest/google-http-client-apache-v2.pom" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client-apache-v2</artifactId>
  <version>$ver</version>
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
      <version>$ver</version>
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
	cat > "$dest/google-http-client-gson.pom" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.http-client</groupId>
  <artifactId>google-http-client-gson</artifactId>
  <version>$ver</version>
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
      <version>$ver</version>
    </dependency>
    <dependency>
      <groupId>com.google.code.gson</groupId>
      <artifactId>gson</artifactId>
      <version>2.14.0</version>
    </dependency>
  </dependencies>
</project>
EOF
}

build_one() {
	root="$1"
	ver="$2"
	ncore="$3"
	dest="$4"
	mkdir -p "$dest"
	find "$root/google-http-client/src/main/java" -name '*.java' > "$dest/core.list"
	test "$(wc -l < "$dest/core.list")" -eq "$ncore"
	mkdir -p "$dest/core-classes"
	javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d "$dest/core-classes" @"$dest/core.list"
	mkdir -p "$dest/core-classes/com/google/api/client/http"
	/bin/cp -f "$root/google-http-client/src/main/resources/com/google/api/client/http/google-http-client.properties" "$dest/core-classes/com/google/api/client/http/"
	cat > "$dest/core.mf" << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client

EOF
	jar cfm "$dest/google-http-client.jar" "$dest/core.mf" -C "$dest/core-classes" .
	jar i "$dest/google-http-client.jar"
	javap -verbose -cp "$dest/google-http-client.jar" com.google.api.client.http.HttpRequest | grep -F 'major version: 55'

	find "$root/google-http-client-apache-v2/src/main/java" -name '*.java' > "$dest/v2.list"
	test "$(wc -l < "$dest/v2.list")" -eq 6
	mkdir -p "$dest/v2-classes"
	javac --release 11 -encoding UTF-8 -Xlint:-options \
		-cp "$dest/google-http-client.jar:$CP" -d "$dest/v2-classes" @"$dest/v2.list"
	cat > "$dest/v2.mf" << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client.http.apache.v2

EOF
	jar cfm "$dest/google-http-client-apache-v2.jar" "$dest/v2.mf" -C "$dest/v2-classes" .
	jar i "$dest/google-http-client-apache-v2.jar"

	find "$root/google-http-client-gson/src/main/java" -name '*.java' > "$dest/gson.list"
	test "$(wc -l < "$dest/gson.list")" -eq 4
	mkdir -p "$dest/gson-classes"
	javac --release 11 -encoding UTF-8 -Xlint:-options \
		-cp "$dest/google-http-client.jar:$CP" -d "$dest/gson-classes" @"$dest/gson.list"
	cat > "$dest/gson.mf" << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client.json.gson

EOF
	jar cfm "$dest/google-http-client-gson.jar" "$dest/gson.mf" -C "$dest/gson-classes" .
	jar i "$dest/google-http-client-gson.jar"
	write_poms "$ver" "$dest"
}

build_one google-http-java-client-1.42.2 1.42.2 157 out142
build_one . %{version} 160 out

%install
set -eo pipefail
for art in google-http-client google-http-client-apache-v2 google-http-client-gson; do
	sysjar install --buildroot %{buildroot} \
		--artifact "out142/$art.pom:out142/$art.jar" \
		--file-name "$art-1.42.2" \
		--filelist ".mfiles142-$art"
	/bin/mv "%{buildroot}/usr/share/sysjar/index/com.google.http-client/$art.sysjar" \
		"%{buildroot}/usr/share/sysjar/index/com.google.http-client/$art-1.42.2.sysjar"
	sed -i "s|/usr/share/sysjar/index/com.google.http-client/$art\\.sysjar|/usr/share/sysjar/index/com.google.http-client/$art-1.42.2.sysjar|" ".mfiles142-$art"
	idx142="%{buildroot}/usr/share/sysjar/index/com.google.http-client/$art-1.42.2.sysjar"
	test -s "$idx142"
	grep -F -q '"version": "1.42.2"' "$idx142"
	grep -F -q "\"artifactId\": \"$art\"" "$idx142"
done
for art in google-http-client google-http-client-apache-v2 google-http-client-gson; do
	sysjar install --buildroot %{buildroot} \
		--artifact "out/$art.pom:out/$art.jar" \
		--file-name "$art" \
		--filelist ".mfiles-$art"
	idx="%{buildroot}/usr/share/sysjar/index/com.google.http-client/$art.sysjar"
	test -s "$idx"
	grep -F -q '"version": "%{version}"' "$idx"
	grep -F -q "\"artifactId\": \"$art\"" "$idx"
	test -s "%{buildroot}%{_javadir}/$art.jar"
	test -s "%{buildroot}%{_javadir}/$art-1.42.2.jar"
done
: > .mfiles
for art in google-http-client google-http-client-apache-v2 google-http-client-gson; do
	while IFS= read -r line; do
		grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
	done < ".mfiles-$art"
	while IFS= read -r line; do
		grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
	done < ".mfiles142-$art"
done

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
		String expect = args[0];
		GenericUrl url = new GenericUrl("https://example.com/gradle");
		if (!"example.com".equals(url.getHost())) {
			throw new RuntimeException("host " + url.getHost());
		}
		if (!expect.equals(HttpRequest.VERSION)) {
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
DEPS=%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar:%{_javadir}/javax.annotation.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/j2objc-annotations.jar:%{_javadir}/opencensus-api.jar:%{_javadir}/opencensus-contrib-http-util.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/error_prone_annotations.jar
run_check() {
	ver="$1"
	core="$2"
	v2="$3"
	gson="$4"
	test -f "$core"
	test -f "$v2"
	test -f "$gson"
	/bin/rm -rf "check/$ver"
	mkdir -p "check/$ver"
	classpath="$core:$v2:$gson:$DEPS"
	javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$classpath" -d "check/$ver" check/Smoke.java
	java -cp "check/$ver:$classpath" Smoke "$ver" > "check/$ver/out.txt"
	cat "check/$ver/out.txt"
	grep -F -q "ghttp_ok $ver /gradle k gradle" "check/$ver/out.txt"
}
run_check %{version} \
	%{buildroot}%{_javadir}/google-http-client.jar \
	%{buildroot}%{_javadir}/google-http-client-apache-v2.jar \
	%{buildroot}%{_javadir}/google-http-client-gson.jar
run_check 1.42.2 \
	%{buildroot}%{_javadir}/google-http-client-1.42.2.jar \
	%{buildroot}%{_javadir}/google-http-client-apache-v2-1.42.2.jar \
	%{buildroot}%{_javadir}/google-http-client-gson-1.42.2.jar

%files -f .mfiles
%doc LICENSE README.md
