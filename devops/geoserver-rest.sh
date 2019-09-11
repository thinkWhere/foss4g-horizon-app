#REST calls

GEOSERVER_PWD=th1nkwhere!
GEOSERVER_URL=http://192.168.16.16
WORKSPACE_NAME=viewpoint
STORE_NAME=viewpoint-store
SCHEMA_NAME=public
DATABASE_HOST=192.168.16.16
DATABASE_NAME=lcdev
DATABASE_USER=viewpoint_user
DATABASE_PWD=viewpoint
LAYER_NAME=viewpoint
TABLE_NAME=viewpoint

# create workspace
PREFIX_XML="<namespace><prefix>$WORKSPACE_NAME</prefix><uri>http://thinkwhere.com/$WORKSPACE_NAME</uri></namespace>"
WORKSPACE_XML="<workspace><name>$WORKSPACE_NAME</name></workspace>"
curl -u admin:$GEOSERVER_PWD -X POST -H "Content-Type: text/xml" -d $PREFIX_XML $GEOSERVER_URL:8080/geoserver/rest/namespaces
curl -u admin:$GEOSERVER_PWD -X POST -H "Content-Type: text/xml" -d $WORKSPACE_XML $GEOSERVER_URL:8080/geoserver/rest/workspaces

#create store
STORE_XML=$(cat <<-END
<dataStore>
    <name>$STORE_NAME</name>
    <description>$STORE_NAME</description>
    <type>PostGIS</type>
    <enabled>true</enabled>
    <workspace>
        <name>$WORKSPACE_NAME</name>
    </workspace>
    <connectionParameters>
        <entry key="schema">$SCHEMA_NAME</entry>
        <entry key="database">$DATABASE_NAME</entry>
        <entry key="host">$DATABASE_HOST</entry>
        <entry key="Loose bbox">true</entry>
        <entry key="Estimated extends">true</entry>
        <entry key="fetch size">1000</entry>
        <entry key="Expose primary keys">true</entry>
        <entry key="Connection timeout">20</entry>
        <entry key="port">5432</entry>
        <entry key="user">$DATABASE_USER</entry>
        <entry key="passwd">$DATABASE_PWD</entry>
        <entry key="min connections">1</entry>
        <entry key="dbtype">postgis</entry>
        <entry key="max connections">5</entry>
    </connectionParameters></dataStore>
END
)
curl -u admin:$GEOSERVER_PWD -X POST -H "Content-Type: text/xml" -d "$STORE_XML" \
$GEOSERVER_URL:8080/geoserver/rest/workspaces/$WORKSPACE_NAME/datastores

#create layer

LAYER_XML=$(cat <<-END
<featureType>
    <name>$LAYER_NAME</name>
    <nativeName>$TABLE_NAME</nativeName>
    <title>$LAYER_NAME</title>
    <srs>EPSG:27700</srs>
	<nativeBoundingBox><minx>0</minx><maxx>700000</maxx><miny>0</miny><maxy>1300000</maxy></nativeBoundingBox>
    <projectionPolicy>FORCE_DECLARED</projectionPolicy>
    <enabled>true</enabled>
    <maxFeatures>1000</maxFeatures>
</featureType>
END
)

curl -u admin:$GEOSERVER_PWD -X POST -H "Content-Type: text/xml" -d "$LAYER_XML" \
$GEOSERVER_URL:8080/geoserver/rest/workspaces/$WORKSPACE_NAME/datastores/$STORE_NAME/featuretypes?recalculate=true
