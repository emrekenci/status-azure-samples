using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Microsoft.WindowsAzure.Storage.Blob;

namespace FunctionApp
{
    public static class BlobTriggeredFunction
    {
        // The name of the function as it will appear in the portal. You can have multiple functions running under the same Function App (the deployment host).
        // The function names must be unique for functions running under the same Function App.
        [FunctionName("BlobTriggeredFunction")]
        // The "source-files" below in BlobTrigger("source-files/{name}" is the name of our blob container.
        // The Connection = "BlobStorage" is the name of our app setting parameter, holding the azure storage connection string.
        public static void Run([BlobTrigger("source-files/{name}", Connection = "BlobStorage")]ICloudBlob blob, string name, ILogger logger)
        {
            logger.LogInformation("Blob " + blob.Name + " was created or edited. Metadata of the file: ");
            
            // The metadata property is a key value dictionary containing the metadata of the file.
            // Check if a file contains a certain metadata using this propery.
            foreach (var metadataItem in blob.Metadata)
            {
                logger.LogInformation(metadataItem.Key + " " + metadataItem.Value);
            }

            /* HOW TO IDENTIFY A FILE FROM IN BLOB STORAGE
             * 
             * The information we need to be able to identify this file are:
             * 
             * 1) The storage account name. The name you gave to your storage account while creating. 
             * This is unique across Azure and easy to see from the portal. As long as you use the same
             * account and hence the same connection string across the application, you don't need to persist
             * this information in the DB.
             * 
             * 2) The blob container that hosts the file. Think of Blob Containers as folders. In the above code,
             * our container name is "source-files"
             * 
             * 3) The blob name. The name of the individual blob. The file name.
             * 
             */

            /* HOW DOES AZURE FUNCTIONS KEEP TRACK OF THE FILES IT PROCESSED
             * 
             * The functions runtime creates a Blob Container called azure-webjobs-host in the storage account we provide to it.
             * In it, it keeps the last scan time information and the list of files it processed.
             * For each environment, the container is different. Local debugging will create a separate Container. Once deployed 
             * the files which were processed locally will be re-processed on Azure.
             */
        }
    }
}