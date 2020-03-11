import React, { useState } from "react";
import {
  Container,
  Segment,
  Grid,
  Button,
  Form,
  Divider,
  Header
} from "semantic-ui-react";

/**
 * (^([\w,.-]+\s)+(\s)+\d{5})+\s+^((\s\[.+\])\s)*
 */

function App() {
  const [url, setUrl] = useState("http://54.159.94.207:5000")
  const [query, setQuery] = useState("");
  const [queryStatus, setStatus] = useState("");
  const [queryCode, setQueryCode] = useState(false);
  const [noteStatus, setNoteStatus] = useState("");
  const [notesText, setNoteText] = useState("");
  const handleSearchChange = e => {
    if (queryStatus !== "" || noteStatus !== "") {
      setStatus("");
      setNoteStatus("");
    }
    setQuery(e.target.value);
  };
  const handleNotesChange = e => {
    setNoteText(e.target.value);
  };
  function clickSearch() {
    fetch(url+"/search?query=" + query)
      .then(response => response.json())
      .then(data => {
        if (data.code === 0) {
          setStatus("No Record Found");
        } else {
          setStatus("Author: " + data.Author);
          setQueryCode(true);
        }
      });
  }
  function clickNotes() {
    if (queryCode) {
      fetch(url+"/notes?keyword=" + query)
        .then(response => response.json())
        .then(data => {
          if (data.code === 0) {
            setNoteStatus("No Notes Found");
          } else {
            setNoteText(data.notes.join("\n\n"));
          }
        });
    }
  }
  function submitNotes() {
    notesText.split("\n\n").forEach(note => {
      fetch(
        url+"/add_note?keyword=" + query + "&note=" + note
      )
        .then(response => response.json())
        .then(data => {
          console.log(data);
        });
    });
  }
  return (
    <Container style={{ margin: 20 }}>
      <Segment>
        <Grid columns={2} relaxed="very" stackable>
          <Grid.Row>
            <Grid.Column>
              <Form>
                <Form.Input
                  icon="search"
                  iconPosition="left"
                  placeholder="Search"
                  value={query}
                  onChange={handleSearchChange}
                />
              </Form>
            </Grid.Column>
            <Grid.Column verticalAlign="middle">
              <Button content="Search" primary onClick={() => clickSearch()} />
              <Button
                content="List Notes"
                primary
                onClick={() => clickNotes()}
                disabled={!queryCode}
              />
            </Grid.Column>
          </Grid.Row>
          <Grid.Row>
            <Grid.Column>
              <Header size="small">{queryStatus}</Header>
            </Grid.Column>
            <Grid.Column>
              <Header size="small">{noteStatus}</Header>
            </Grid.Column>
          </Grid.Row>
          <Grid.Row>
            <Grid.Column>
              <Form.TextArea
                id="form-note"
                placeholder="Notes"
                value={notesText}
                onChange={handleNotesChange}
                rows='15'
                style={{'width': '100%'}}
              />
            </Grid.Column>
            <Grid.Column>
              <Button
                content="Submit Notes"
                onClick={() => submitNotes()}
                primary
                disabled={!queryCode}
              />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Segment>
    </Container>
  );
}

export default App;
