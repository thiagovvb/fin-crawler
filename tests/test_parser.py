from src.parser import PageParser

HTML_OK = """
<html>
  <body>
    <table>
      <tbody>
        <tr>
          <td>1</td>
          <td>ABCD3</td>
          <td>Empresa ABC</td>
          <td>Setor</td>
          <td>12.34</td>
        </tr>
        <tr>
          <td>2</td>
          <td>EFGH4</td>
          <td>Empresa EFG</td>
          <td>Setor</td>
          <td>56.78</td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
"""

HTML_NOPRICE = """
<html>
  <body>
    <table>
      <tbody>
        <tr>
          <td>1</td>
          <td>ABCD3</td>
          <td>Empresa ABC</td>
          <td>Setor</td>
          <td>12.34</td>
        </tr>
        <tr>
          <td>2</td>
          <td>EFGH4</td>
          <td>Empresa EFG</td>
          <td>Setor</td>
          <td>N/A</td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
"""

HTML_NO_TABLE = "<html><body><p>Sem tabela</p></body></html>"

def test_extract_table_data_ok():
    parser = PageParser()
    data = parser.extract_table_data(HTML_OK)
    assert len(data) == 2
    assert data[0]["symbol"] == "ABCD3"
    assert data[0]["name"] == "Empresa ABC"
    assert data[0]["price"] == 12.34

def test_extract_table_data_no_table():
    parser = PageParser()
    data = parser.extract_table_data(HTML_NO_TABLE)

    assert data == []

def test_invalid_price():
    parser = PageParser()
    data = parser.extract_table_data(HTML_NOPRICE)
    assert data[1]["symbol"] == "EFGH4"
    assert data[1]["name"] == "Empresa EFG"
    assert data[1]["price"] is None