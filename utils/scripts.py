class Scripts(objects):
    
    private static void downloadPartScripts(int familyIndex)
        {
            byte[] commandArray = new byte[1];
            commandArray[0] = KONST.CLR_SCRIPT_BUFFER;      // clear script buffer- we're loading new scripts
            bool result = writeUSB(commandArray);
            
            // clear the script redirect table
            for (int i = 0; i < scriptRedirectTable.Length; i++)
            {
                scriptRedirectTable[i].redirectToScriptLocation = 0;
                scriptRedirectTable[i].deviceFileScriptNumber = 0;
            }

            // program entry
            if (DevFile.Families[familyIndex].ProgEntryScript != 0) // don't download non-existant scripts
            {
                if (lvpEnabled && (DevFile.PartsList[ActivePart].LVPScript > 0))
                {
                    downloadScript(KONST.PROG_ENTRY, DevFile.PartsList[ActivePart].LVPScript);
                }
                else if (vppFirstEnabled && (DevFile.Families[familyIndex].ProgEntryVPPScript != 0))
                { // download VPP first program mode entry
                    downloadScript(KONST.PROG_ENTRY, DevFile.Families[familyIndex].ProgEntryVPPScript);
                }
                else
                { // standard program entry
                    downloadScript(KONST.PROG_ENTRY, DevFile.Families[familyIndex].ProgEntryScript);
                }
            }
            // program exit
            if (DevFile.Families[familyIndex].ProgExitScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.PROG_EXIT, DevFile.Families[familyIndex].ProgExitScript);
            }
            // read device id
            if (DevFile.Families[familyIndex].ReadDevIDScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.RD_DEVID, DevFile.Families[familyIndex].ReadDevIDScript);
            }
            // read program memory
            if (DevFile.PartsList[ActivePart].ProgMemRdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.PROGMEM_RD, DevFile.PartsList[ActivePart].ProgMemRdScript);
            }
            // chip erase prep
            if (DevFile.PartsList[ActivePart].ChipErasePrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.ERASE_CHIP_PREP, DevFile.PartsList[ActivePart].ChipErasePrepScript);
            }            
            // set program memory address
            if (DevFile.PartsList[ActivePart].ProgMemAddrSetScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.PROGMEM_ADDRSET, DevFile.PartsList[ActivePart].ProgMemAddrSetScript);
            }
            // prepare for program memory write
            if (DevFile.PartsList[ActivePart].ProgMemWrPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.PROGMEM_WR_PREP, DevFile.PartsList[ActivePart].ProgMemWrPrepScript);
            }
            // program memory write                 
            if (DevFile.PartsList[ActivePart].ProgMemWrScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.PROGMEM_WR, DevFile.PartsList[ActivePart].ProgMemWrScript);
            }
            // prep for ee read               
            if (DevFile.PartsList[ActivePart].EERdPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.EE_RD_PREP, DevFile.PartsList[ActivePart].EERdPrepScript);
            }
            // ee read               
            if (DevFile.PartsList[ActivePart].EERdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.EE_RD, DevFile.PartsList[ActivePart].EERdScript);
            }
            // prep for ee write               
            if (DevFile.PartsList[ActivePart].EEWrPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.EE_WR_PREP, DevFile.PartsList[ActivePart].EEWrPrepScript);
            }
            // ee write               
            if (DevFile.PartsList[ActivePart].EEWrScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.EE_WR, DevFile.PartsList[ActivePart].EEWrScript);
            }
            // prep for config read       
            if (DevFile.PartsList[ActivePart].ConfigRdPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.CONFIG_RD_PREP, DevFile.PartsList[ActivePart].ConfigRdPrepScript);
            }
            // config read       
            if (DevFile.PartsList[ActivePart].ConfigRdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.CONFIG_RD, DevFile.PartsList[ActivePart].ConfigRdScript);
            }
            // prep for config write       
            if (DevFile.PartsList[ActivePart].ConfigWrPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.CONFIG_WR_PREP, DevFile.PartsList[ActivePart].ConfigWrPrepScript);
            }
            // config write       
            if (DevFile.PartsList[ActivePart].ConfigWrScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.CONFIG_WR, DevFile.PartsList[ActivePart].ConfigWrScript);
            }
            // prep for user id read      
            if (DevFile.PartsList[ActivePart].UserIDRdPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.USERID_RD_PREP, DevFile.PartsList[ActivePart].UserIDRdPrepScript);
            }
            // user id read      
            if (DevFile.PartsList[ActivePart].UserIDRdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.USERID_RD, DevFile.PartsList[ActivePart].UserIDRdScript);
            }
            // prep for user id write      
            if (DevFile.PartsList[ActivePart].UserIDWrPrepScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.USERID_WR_PREP, DevFile.PartsList[ActivePart].UserIDWrPrepScript);
            }
            // user id write      
            if (DevFile.PartsList[ActivePart].UserIDWrScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.USERID_WR, DevFile.PartsList[ActivePart].UserIDWrScript);
            }
            // read osscal      
            if (DevFile.PartsList[ActivePart].OSCCALRdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.OSSCAL_RD, DevFile.PartsList[ActivePart].OSCCALRdScript);
            }
            // write osscal      
            if (DevFile.PartsList[ActivePart].OSCCALWrScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.OSSCAL_WR, DevFile.PartsList[ActivePart].OSCCALWrScript);
            }
            // chip erase      
            if (DevFile.PartsList[ActivePart].ChipEraseScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.ERASE_CHIP, DevFile.PartsList[ActivePart].ChipEraseScript);
            }
            // program memory erase 
            if (DevFile.PartsList[ActivePart].ProgMemEraseScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.ERASE_PROGMEM, DevFile.PartsList[ActivePart].ProgMemEraseScript);
            }
            // ee erase 
            if (DevFile.PartsList[ActivePart].EEMemEraseScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.ERASE_EE, DevFile.PartsList[ActivePart].EEMemEraseScript);
            }
            // row erase
            if (DevFile.PartsList[ActivePart].DebugRowEraseScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.ROW_ERASE, DevFile.PartsList[ActivePart].DebugRowEraseScript);
            }            
            // Test Memory Read
            if (DevFile.PartsList[ActivePart].TestMemoryRdScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.TESTMEM_RD, DevFile.PartsList[ActivePart].TestMemoryRdScript);
            }
            // EE Row Erase
            if (DevFile.PartsList[ActivePart].EERowEraseScript != 0) // don't download non-existant scripts
            {
                downloadScript(KONST.EEROW_ERASE, DevFile.PartsList[ActivePart].EERowEraseScript);
            }            
            
            // get script buffer checksum
             scriptBufferChecksum = getScriptBufferChecksum();
        }
        
