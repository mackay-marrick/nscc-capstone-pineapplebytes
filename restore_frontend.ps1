$files = @(
    'src/app/page.tsx',
    'src/app/layout.tsx',
    'src/app/globals.css',
    'src/app/favicon.ico',
    'src/components/RestaurantHeader.tsx',
    'src/components/OverviewView.tsx',
    'src/components/SummaryView.tsx',
    'src/components/RestaurantSelector.tsx',
    'src/data/restaurantData.ts',
    'src/lib/utils.ts',
    'eslint.config.mjs',
    'next.config.ts',
    'package.json',
    'postcss.config.mjs',
    'tailwind.config.ts',
    'tsconfig.json',
    'public/file.svg',
    'public/globe.svg',
    'public/next.svg',
    'public/vercel.svg',
    'public/window.svg',
    'sql_files/pineapplebites_agreement.sql',
    'sql_files/pineapplebites_company.sql',
    'sql_files/pineapplebites_configuration.sql',
    'sql_files/pineapplebites_contact.sql',
    'sql_files/pineapplebites_resource.sql',
    'sql_files/pineapplebites_team.sql',
    'sql_files/pineapplebites_ticket.sql',
    '.gitignore',
    'README.md'
)

foreach ($file in $files) {
    $content = git show a6a0013:"$file" 2>$null
    if ($content -and $content.Trim() -ne '') {
        $path = Join-Path 'pineapplebytes_nscc_capstone' $file
        $dir = Split-Path $path -Parent
        if (!(Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
        }
        Set-Content -Path $path -Value $content -Encoding UTF8
        Write-Host "Created: $file"
    } else {
        Write-Host "FAILED: $file"
    }
}