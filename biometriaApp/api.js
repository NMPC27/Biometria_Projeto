const endpoint = "https://biometriapp.nunompcunha2001.workers.dev"
const TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTkxMTAzMDAsImV4cCI6MTczMDY0NjMwMCwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.lRJ3CpOEdegZ4d45xTtUx3VvboPMcl4LQcvVv79IL0s"

export default async function sendId(id){
    fetch(endpoint, {
        method: 'POST',
        headers: {},
        body: JSON.stringify({"token": TOKEN, "id": id}) 
    }).catch(error => {
        console.error(error);
    });
}
