---
source_url: https://beam.apache.org/documentation/io/built-in/hcatalog/
fetched_at_utc: 2026-03-07T12:12:29.230731+00:00
page_title: "Apache HCatalog I/O connector"
beam_last_updated: "Last updated on 2026/03/06"
---

# HCatalog IO

An `HCatalogIO` is a transform for reading and writing data to an HCatalog managed source.

### Reading using HCatalogIO

To configure an HCatalog source, you must specify a metastore URI and a table name. Other optional parameters are database and filter.

For example:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support HCatalogIO.
```

### Writing using HCatalogIO

To configure an `HCatalog` sink, you must specify a metastore URI and a table name. Other
optional parameters are database, partition and batchsize.
The destination table should exist beforehand as the transform will not create a new table if missing.

For example:

![](/images/copy-icon.svg)

```
  # The Beam SDK for Python does not support HCatalogIO.
```

### Using older versions of HCatalog (1.x)

`HCatalogIO` is built for Apache HCatalog versions 2 and up and will not work out of the box for older versions of HCatalog.
The following illustrates a workaround to work with Hive 1.1.

Include the following Hive 1.2 jars in the uber jar you build.
The 1.2 jars provide the necessary methods for Beam while remain compatible with Hive 1.1.

```
<dependency>
    <groupId>org.apache.beam</groupId>
    <artifactId>beam-sdks-java-io-hcatalog</artifactId>
    <version>${beam.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.hive.hcatalog</groupId>
    <artifactId>hive-hcatalog-core</artifactId>
    <version>1.2</version>
</dependency>
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-metastore</artifactId>
    <version>1.2</version>
</dependency>
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-exec</artifactId>
    <version>1.2</version>
</dependency>
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-common</artifactId>
    <version>1.2</version>
</dependency>
```

Relocate _only_ the following hive packages:

```
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>${maven-shade-plugin.version}</version>
    <configuration>
        <createDependencyReducedPom>false</createDependencyReducedPom>
        <filters>
            <filter>
                <artifact>*:*</artifact>
                <excludes>
                    <exclude>META-INF/*.SF</exclude>
                    <exclude>META-INF/*.DSA</exclude>
                    <exclude>META-INF/*.RSA</exclude>
                </excludes>
            </filter>
        </filters>
    </configuration>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <shadedArtifactAttached>true</shadedArtifactAttached>
                <shadedClassifierName>shaded</shadedClassifierName>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                </transformers>
                <relocations>
                    <!-- Important: Do not relocate org.apache.hadoop.hive -->
                    <relocation>
                        <pattern>org.apache.hadoop.hive.conf</pattern>
                        <shadedPattern>h12.org.apache.hadoop.hive.conf</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>org.apache.hadoop.hive.ql</pattern>
                        <shadedPattern>h12.org.apache.hadoop.hive.ql</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>org.apache.hadoop.hive.metastore</pattern>
                        <shadedPattern>h12.org.apache.hadoop.hive.metastore</shadedPattern>
                    </relocation>
                </relocations>
            </configuration>
        </execution>
    </executions>
</plugin>
```

This has been testing to read SequenceFile and ORCFile file backed tables running with
Beam 2.4.0 on Spark 2.3 / YARN in a Cloudera CDH 5.12.2 managed environment.
