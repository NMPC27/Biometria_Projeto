import React, {useState} from 'react';
import {View, Text, StyleSheet, Button} from 'react-native';
import NfcManager, {NfcTech} from 'react-native-nfc-manager';
import sendId from './api';

// Pre-step, call this before any NFC operations
NfcManager.start();

function App() {

  const [print, setPrint] = useState('---');

  async function readNdef() {
    try {
      // register for the NFC tag with NDEF in it
      await NfcManager.requestTechnology(NfcTech.Ndef);
      // the resolved tag object will contain `ndefMessage` property
      const tag = await NfcManager.getTag();

      setPrint(tag.id);
      sendId(tag.id);
    } catch (ex) {
      setPrint("ERROR!");
    } finally {
      // stop the nfc scanning
      NfcManager.cancelTechnologyRequest();
    }
  
  }

  return (
    <>
    <View style={styles.wrapper}>
      <Button
        onPress={readNdef}
        title="Scan a Tag"
      />

      <Text>{print}</Text>
    </View>
    <View style={{flex: 2 }} /> 
    </>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  }
});

export default App;