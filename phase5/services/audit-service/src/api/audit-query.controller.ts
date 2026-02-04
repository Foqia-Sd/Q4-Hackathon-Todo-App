import { AuditQueryService, AuditFilter } from '../services/audit-query.service';
import { AuditEntry } from '../models/audit-entry';

export class AuditQueryController {
  private auditQueryService: AuditQueryService;

  constructor(auditQueryService: AuditQueryService) {
    this.auditQueryService = auditQueryService;
  }

  /**
   * Get audit entries for a specific task ID
   * @param taskId The task ID to query audits for
   * @returns Array of audit entries
   */
  async getAuditsByTaskId(taskId: string): Promise<AuditEntry[]> {
    if (!taskId) {
      throw new Error('Task ID is required');
    }

    return await this.auditQueryService.getAuditsByTaskId(taskId);
  }

  /**
   * Get audit entries by various filters
   * @param filter Filter options
   * @returns Array of audit entries
   */
  async getAuditsByFilter(filter: AuditFilter): Promise<AuditEntry[]> {
    return await this.auditQueryService.getAuditsByFilter(filter);
  }

  /**
   * Get audit entries by user ID
   * @param userId The user ID to query audits for
   * @returns Array of audit entries
   */
  async getAuditsByUserId(userId: string): Promise<AuditEntry[]> {
    if (!userId) {
      throw new Error('User ID is required');
    }

    return await this.auditQueryService.getAuditsByUserId(userId);
  }
}