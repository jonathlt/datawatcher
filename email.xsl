<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>Comparison Results</h2>
    <table border="0">
      <xsl:choose>
      <xsl:when test="count(table/rows/row) > 0">
      	<xsl:apply-templates select="table/rows/row"/>
      </xsl:when>
      <xsl:otherwise>
        No differences found for this comparison
      </xsl:otherwise>
      </xsl:choose>
    </table>
  </body>
  </html>
</xsl:template>

<xsl:template match="row">
	
	<xsl:if test="position()=1">
	<tr bgcolor="#9acd32">
		<xsl:for-each select="*">
	  		<th><xsl:value-of select="name()"/></th>
		</xsl:for-each>
	</tr>
	</xsl:if>
	<tr>
	<xsl:for-each select="*">
		<td><xsl:value-of select="."/></td>
	</xsl:for-each>
	</tr>
</xsl:template>

</xsl:stylesheet>
