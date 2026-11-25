INSERT INTO storage (
    TimestampCreated,
    TimestampModified,
    version,
    Abbrev,
    FullName,
    HighestChildNodeNumber,
    IsAccepted,
    Name,
    NodeNumber,
    Number1,
    Number2,
    RankID,
    Remarks,
    Text1,
    Text2,
    TimestampVersion,
    StorageTreeDefID,
    ModifiedByAgentID,
    AcceptedID,
    ParentID,
    StorageTreeDefItemID,
    CreatedByAgentID,
    UniqueIdentifier
)
SELECT
    NOW(),
    NOW(),
    1,
    NULL,
    LPAD(@n:=@n+1,3,'0'),
    NULL,
    b'1',
    LPAD(@n,3,'0'),
    61584 + @n,      -- Ensure correct highest child node number plus one!
    NULL,
    NULL,
    400,   -- Ensure correct rank ID! 
    NULL,
    NULL,
    NULL,
    NULL,
    1,
    10215,
    NULL,
    437054,
    8,     -- Match rank ID! 
    10215,
    UUID()
FROM storage
CROSS JOIN (SELECT @n:=0) vars
LIMIT 864;